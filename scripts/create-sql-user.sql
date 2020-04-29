DROP USER 'sailshift_user';
CREATE USER 'sailshift_user' IDENTIFIED BY 'sailshift_password';
GRANT ALL PRIVILEGES ON sailshift.* TO 'sailshift_user';
FLUSH PRIVILEGES;
