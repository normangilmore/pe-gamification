-- Sanitize sensitive columns in a Pybossa database
update project set secret_key = '';
update project set info = '{}';
update project set webhook='';

update "user" set passwd_hash = "user".id;
update "user" set api_key = "user".id;
update "user" set email_addr = "user".id;
update "user" set name="user".id;
update "user" set fullname="user".id;

-- Just tidying.
truncate auditlog;
truncate announcement;
truncate blogpost;
