SELECT domain, COUNT(domain) AS domain_count
FROM users
GROUP BY domain
ORDER BY domain_count DESC
LIMIT 1;
