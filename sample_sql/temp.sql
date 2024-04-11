
Select 
    e.EmployeeID,
    e.EmployeeName,
    e.Role,
    d.DepartmentName,
    d.DepartmentLocation
FROM
    Employee e
JOIN
    Department d
ON
    e.DepartmentID = d.DepartmentID
WHERE
    d.DepartmentLocation = 'New York'
ORDER BY
    e.EmployeeName;

-- # Actual Upgrade Result (Jan 2023)
-- select boss_id, pack_type, contract_start,DATE_ADD(contract_start, 
-- INTERVAL 30 DAY) as contract_start_30day,effective_date
-- from 
-- `tvb-crs-pro.mytvsuper_report.boss_cid_subscription_20230228`where 
-- pack_type in ('mytv_gold', 'mytv_gold_top_up_premium', 
-- 'silver_top_up_premium')and boss_id not in (
-- select distinct boss_id from 
-- `tvb-crs-pro.mytvsuper_report.boss_cid_subscription_20230131`
-- where pack_type in ('mytv_gold', 'mytv_gold_top_up_premium', 
-- 'silver_top_up_premium'))


-- WITH RankedOrders AS (
--     SELECT
--         o.OrderID,
--         o.CustomerID,
--         o.OrderDate,
--         od.ProductID,
--         od.UnitPrice,
--         od.Quantity,
--         SUM(od.UnitPrice * od.Quantity) OVER (PARTITION BY o.CustomerID ORDER BY o.OrderDate) AS RunningTotal,
--         ROW_NUMBER() OVER (PARTITION BY o.CustomerID ORDER BY o.OrderDate DESC) AS RecentOrderRank
--     FROM
--         Orders o
--     INNER JOIN OrderDetails od ON o.OrderID = od.OrderID
--     WHERE
--         o.OrderDate BETWEEN '2023-01-01' AND '2023-12-31'
-- ),
-- TopCustomers AS (
--     SELECT
--         CustomerID,
--         SUM(UnitPrice * Quantity) AS TotalSpent
--     FROM
--         RankedOrders
--     GROUP BY
--         CustomerID
--     HAVING
--         SUM(UnitPrice * Quantity) > 1000
-- )
-- SELECT
--     r.CustomerID,
--     r.OrderID,
--     r.OrderDate,
--     r.ProductID,
--     r.UnitPrice,
--     r.Quantity,
--     r.RunningTotal
-- FROM
--     RankedOrders r
-- INNER JOIN TopCustomers tc ON r.CustomerID = tc.CustomerID
-- WHERE
--     r.RecentOrderRank = 1
-- ORDER BY
--     r.CustomerID,
--     r.OrderDate DESC;
