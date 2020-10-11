\timing on

-- What categories do we have?
SELECT id, name
FROM category;

-- How are projects linked to categories?
SELECT category_id, id
FROM project;

-- How many projects in each category?
SELECT category_id, count(id)
FROM project
GROUP BY category_id;

-- tidy WITH a sort
SELECT category_id, count(id)
FROM project
GROUP BY category_id
ORDER BY category_id;

-- Let's join the category table so we can show the category name
SELECT p.category_id, c.name, count(p.id)
FROM project p
JOIN category c on c.id=p.category_id
GROUP BY p.category_id, c.name
ORDER BY p.category_id;

-- What projects are in these categories?
SELECT id, name FROM project WHERE category_id = 3;
SELECT id, name FROM project WHERE category_id = 2;

-- We'll ignore categories for now, but when projects are organized
-- into categories, we'll want to only process projects in a given
-- list of categories.
SELECT id, name
FROM project
WHERE category_id IN (2, 3);

-- Let's take a look at the task_run table.
-- What does it look like?
SELECT project_id, user_id FROM task_run;

-- How many?
SELECT count(*) FROM task_run;

-- Tally task_runs by project, by user.
SELECT project_id, user_id, count(*)
FROM task_run
GROUP BY project_id, user_id;

-- label column
SELECT project_id, user_id, count(*) completed
FROM task_run
GROUP BY project_id, user_id;

-- sort by count to get a sense of range
SELECT project_id, user_id, count(*) completed
FROM task_run
GROUP BY project_id, user_id
ORDER BY completed;

-- Just ones that meet threshold
SELECT project_id, user_id, count(*) completed
FROM task_run
GROUP BY project_id, user_id
HAVING count(*) >= 25
ORDER BY completed;

-- Show individual level awards
SELECT project_id, user_id, count(*) completed,
CASE
  WHEN count(*) >= 25 then TRUE
  ELSE FALSE
END bronze,
CASE
  WHEN count(*) >= 50 then TRUE
  ELSE FALSE
END silver
FROM task_run
GROUP BY project_id, user_id
HAVING count(*) >= 25
ORDER BY completed;

-- Let's track awards given so far.
CREATE TEMPORARY TABLE awards (badge_id INTEGER, user_id INTEGER, project_id INTEGER, reason VARCHAR(32));
INSERT INTO awards VALUES (1000, 205, 220, 'INDIVIDUAL');

SELECT * FROM awards;

-- Same query, hoisted into a CTE
WITH earnable_badges as (
  SELECT project_id, user_id, count(*) completed,
  CASE
    WHEN count(*) >= 25 then TRUE
    ELSE FALSE
  END bronze,
  CASE
    WHEN count(*) >= 50 then TRUE
    ELSE FALSE
  END silver
  FROM task_run
  GROUP BY project_id, user_id
  HAVING count(*) >= 25
  ORDER BY completed
)
SELECT * FROM earnable_badges;

-- add a subquery column showing if badge awarded already
WITH earnable_badges as (
  SELECT project_id, user_id, count(*) completed,
  CASE
    WHEN count(*) >= 25 then TRUE
    ELSE FALSE
  END bronze,
  CASE
    WHEN count(*) >= 50 then TRUE
    ELSE FALSE
  END silver
  FROM task_run
  GROUP BY project_id, user_id
  HAVING count(*) >= 25
  ORDER BY completed
)
SELECT project_id, user_id, completed, bronze, silver, exists (
  SELECT * FROM awards
  WHERE awards.project_id = earnable_badges.project_id AND
        awards.user_id = earnable_badges.user_id
) awarded
FROM earnable_badges;

-- Move subquery column to WHERE clause and filter out already awarded badges
WITH earnable_badges as (
  SELECT project_id, user_id, count(*) completed,
  CASE
    WHEN count(*) >= 25 then TRUE
    ELSE FALSE
  END bronze,
  CASE
    WHEN count(*) >= 50 then TRUE
    ELSE FALSE
  END silver
  FROM task_run
  GROUP BY project_id, user_id
  HAVING count(*) >= 25
  ORDER BY completed
)
SELECT project_id, user_id, completed, bronze, silver
FROM earnable_badges
WHERE not exists (
  SELECT * FROM awards
  WHERE awards.project_id = earnable_badges.project_id AND
        awards.user_id = earnable_badges.user_id
);

-- Another way to write the above query, without a correlated subquery
-- Change not exists correlated subquery to a left join
-- WHERE we keep the columns that do NOT sucessfully join to awards
-- i.e., not exists
WITH earnable_badges as (
  SELECT project_id, user_id, count(*) completed,
  CASE
    WHEN count(*) >= 25 then TRUE
    ELSE FALSE
  END bronze,
  CASE
    WHEN count(*) >= 50 then TRUE
    ELSE FALSE
  END silver
  FROM task_run
  GROUP BY project_id, user_id
  HAVING count(*) >= 25
  ORDER BY completed
)
SELECT e.project_id, e.user_id, e.completed, e.bronze, e.silver
FROM earnable_badges e
left join awards on
  awards.project_id = e.project_id AND
  awards.user_id = e.user_id
WHERE awards.project_id is null;

-- Move this entire query into a CTE
WITH awardable_badges as (
  WITH earnable_badges as (
    SELECT project_id, user_id, count(*) completed,
    CASE
      WHEN count(*) >= 25 then TRUE
      ELSE FALSE
    END bronze,
    CASE
      WHEN count(*) >= 50 then TRUE
      ELSE FALSE
    END silver
    FROM task_run
    GROUP BY project_id, user_id
    HAVING count(*) >= 25
    ORDER BY completed
  )
  SELECT project_id, user_id, completed, bronze, silver
  FROM earnable_badges
  WHERE not exists (
    SELECT * FROM awards
    WHERE awards.project_id = earnable_badges.project_id AND
          awards.user_id = earnable_badges.user_id
  )
)
SELECT * FROM awardable_badges;


-- Let's just keep the silver that are due to be awarded, and
-- include the silver badge id in the result rows
WITH awardable_badges as (
  WITH earnable_badges as (
    SELECT project_id, user_id, count(*) completed,
    CASE
      WHEN count(*) >= 25 then TRUE
      ELSE FALSE
    END bronze,
    CASE
      WHEN count(*) >= 50 then TRUE
      ELSE FALSE
    END silver
    FROM task_run
    GROUP BY project_id, user_id
    HAVING count(*) >= 25
    ORDER BY completed
  )
  SELECT project_id, user_id, completed, bronze, silver
  FROM earnable_badges
  WHERE not exists (
    SELECT * FROM awards
    WHERE awards.project_id = earnable_badges.project_id AND
          awards.user_id = earnable_badges.user_id
  )
)
SELECT 1001, user_id, project_id, 'SILVER' FROM awardable_badges ab
WHERE ab.silver = True;


-- Let's insert the above result directly into the awarded table.
-- Put whole query above in another CTE
WITH awardable_badges as (
  WITH earnable_badges as (
    SELECT project_id, user_id, count(*) completed,
    CASE
      WHEN count(*) >= 25 then TRUE
      ELSE FALSE
    END bronze,
    CASE
      WHEN count(*) >= 50 then TRUE
      ELSE FALSE
    END silver
    FROM task_run
    GROUP BY project_id, user_id
    HAVING count(*) >= 25
    ORDER BY completed
  )
  SELECT project_id, user_id, completed, bronze, silver
  FROM earnable_badges
  WHERE not exists (
    SELECT * FROM awards
    WHERE awards.project_id = earnable_badges.project_id AND
          awards.user_id = earnable_badges.user_id
  )
)
INSERT INTO awards (badge_id, user_id, project_id, reason)
  SELECT 1001, user_id, project_id, 'SILVER' FROM awardable_badges ab
  WHERE ab.silver = True;
;

-- Ok the above ends our discussion of individual achievements.
-- Now we want to consider awards based on user's competitive standing.
-- How do we determine which user was first to complete 25 task runs for
-- each project?

-- Let's try this.
-- What is the last time each user finished a task_run for each project
-- they contributed to?
-- GROUP BY is not going to work for finding a user's Nth contribution.
-- This is not going to tell us who was first to 25.
WITH earnable_badges as (
  SELECT project_id, user_id, count(*) completed, max(finish_time) user_finish
  FROM task_run
  GROUP BY project_id, user_id
  HAVING count(*) >= 25
  ORDER BY user_finish
)
SELECT project_id, user_id, completed, user_finish
FROM earnable_badges
;

-- Let's define a WINDOW so we can rank order rows with the RANK window function.
  SELECT project_id, user_id, RANK() over w, finish_time
  FROM task_run
  WINDOW w as (ORDER BY finish_time)
;

-- Let's GROUP BY project_id
  SELECT project_id, user_id, RANK() over w, finish_time
  FROM task_run
  WINDOW w as (PARTITION BY project_id ORDER BY finish_time)
  ORDER BY project_id
;

-- Ok, we need to GROUP BY project_id and user_id
  SELECT project_id, user_id, RANK() over w, finish_time
  FROM task_run
  WINDOW w as (
    PARTITION BY project_id, user_id
    ORDER BY finish_time
  )
  ORDER BY project_id, user_id
;

-- Let's put this in a CTE so we can filter by rank
-- Now we can see what time each user contributed their 25th task.
-- And we can see what order the 25th tasks were submitted by users
-- by switching sort to finish_time
WITH ranked_taskruns as (
  SELECT project_id, user_id, RANK() over w user_rank, finish_time
  FROM task_run
  WINDOW w as (
    PARTITION BY project_id, user_id
    ORDER BY finish_time
  )
  ORDER BY finish_time
)
SELECT *
FROM ranked_taskruns
WHERE user_rank=25
;

-- Let's apply a WINDOW function over projects to see who
-- was the first person to contribute 25 tasks to a project.
-- and let's add a finish_order to keep track
WITH ranked_taskruns as (
  SELECT project_id, user_id, RANK() over w user_rank, finish_time
  FROM task_run
  WINDOW w as (PARTITION BY project_id, user_id ORDER BY finish_time)
  ORDER BY project_id, user_id
)
SELECT project_id, user_id, user_rank, finish_time,
       RANK() over w2 finish_order,
       FIRST_VALUE(user_id) OVER w2 first_user_id,
       FIRST_VALUE(finish_time) OVER w2 first_finish_time
FROM ranked_taskruns
WHERE user_rank=25
WINDOW w2 as (
  PARTITION BY project_id
  ORDER BY finish_time
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
ORDER BY project_id, finish_time
;

-- Push the above query into a CTE, you knew we were gonna do that
WITH project_achievements as (
  WITH ranked_taskruns as (
    SELECT project_id, user_id, RANK() over w user_rank, finish_time
    FROM task_run
    WINDOW w as (PARTITION BY project_id, user_id ORDER BY finish_time)
    ORDER BY project_id, user_id
  )
  SELECT project_id, user_id, user_rank, finish_time,
         RANK() over w2 finish_order,
         FIRST_VALUE(user_id) OVER w2 first_user_id,
         FIRST_VALUE(finish_time) OVER w2 first_finish_time
  FROM ranked_taskruns
  WHERE user_rank=25
  WINDOW w2 as (
    PARTITION BY project_id
    ORDER BY finish_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  )
  ORDER BY project_id, finish_time
)
SELECT * FROM project_achievements
;

-- Filter to just the first to get an achievement for each project
WITH project_achievements as (
  WITH ranked_taskruns as (
    SELECT project_id, user_id, RANK() over w user_rank, finish_time
    FROM task_run
    WINDOW w as (PARTITION BY project_id, user_id ORDER BY finish_time)
    ORDER BY project_id, user_id
  )
  SELECT project_id, user_id, user_rank, finish_time,
         RANK() over w2 finish_order,
         FIRST_VALUE(user_id) OVER w2 first_user_id,
         FIRST_VALUE(finish_time) OVER w2 first_finish_time
  FROM ranked_taskruns
  WHERE user_rank=25
  WINDOW w2 as (
    PARTITION BY project_id
    ORDER BY finish_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  )
  ORDER BY finish_time
)
SELECT * FROM project_achievements
WHERE finish_order=1
;
