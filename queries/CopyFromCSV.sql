COPY users(user_id, name, email, signup_date, domain)
FROM 'C:\Users\Mykola\PycharmProjects\InforceDataEngineeringTechTask\data\updated_user_data.csv'
delimiter ','
csv
header