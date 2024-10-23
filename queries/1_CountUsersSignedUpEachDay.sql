SELECT signup_date, COUNT(user_id) AS signup_count
FROM users
GROUP BY signup_date;