-- Select the origin and sum of fans for each origin, aliasing the sum as nb_fans
SELECT origin, SUM(nb_fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
