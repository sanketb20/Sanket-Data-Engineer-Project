-- ==========================================
-- A4 PostgreSQL Verification Queries
-- ==========================================

-- Step 1: Total records
SELECT COUNT(*) AS total_records
FROM public.shipments;


-- Step 2: View all loaded shipments
SELECT *
FROM public.shipments
ORDER BY shipment_id;


-- Step 3: Verify rejected records were not loaded
SELECT COUNT(*) AS rejected_records_loaded
FROM public.shipments
WHERE shipment_id IN (
    'SHP1006',
    'SHP1007',
    'SHP1022',
    'SHP1030',
    'SHP1031',
    'SHP1035',
    'SHP1038'
);


-- Step 4: Verify the PostgreSQL shipments table structure and column data types.
-- This confirms that the target table was created with the expected schema.
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'shipments'
ORDER BY ordinal_position;


-- Step 5: Verify that required fields in the loaded records are not NULL.
-- Expected result: 0 for all required fields.
SELECT
    COUNT(*) FILTER (WHERE shipment_id IS NULL) AS null_shipment_id,
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_id,
    COUNT(*) FILTER (WHERE shipment_date IS NULL) AS null_shipment_date,
    COUNT(*) FILTER (WHERE weight_kg IS NULL) AS null_weight_kg
FROM public.shipments;


-- Step 6: Check for duplicate shipment IDs in the loaded data.
-- Expected result: no rows, meaning every shipment_id is unique.
SELECT
    shipment_id,
    COUNT(*) AS occurrence_count
FROM public.shipments
GROUP BY shipment_id
HAVING COUNT(*) > 1
ORDER BY shipment_id;


-- Step 7: Verify the distribution of shipment statuses.
-- This confirms that the loaded records contain the expected status values.
SELECT
    status,
    COUNT(*) AS record_count
FROM public.shipments
GROUP BY status
ORDER BY status;


-- Step 8: Check for NULL values in important shipment columns.
-- This verifies that required fields were loaded without missing values.

SELECT
    COUNT(*) FILTER (WHERE shipment_id IS NULL) AS null_shipment_id,
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_id,
    COUNT(*) FILTER (WHERE shipment_date IS NULL) AS null_shipment_date,
    COUNT(*) FILTER (WHERE origin IS NULL) AS null_origin,
    COUNT(*) FILTER (WHERE destination IS NULL) AS null_destination,
    COUNT(*) FILTER (WHERE status IS NULL) AS null_status,
    COUNT(*) FILTER (WHERE weight_kg IS NULL) AS null_weight_kg,
    COUNT(*) FILTER (WHERE shipping_cost IS NULL) AS null_shipping_cost,
    COUNT(*) FILTER (WHERE carrier IS NULL) AS null_carrier,
    COUNT(*) FILTER (WHERE delivery_date IS NULL) AS null_delivery_date,
    COUNT(*) FILTER (WHERE priority IS NULL) AS null_priority,
    COUNT(*) FILTER (WHERE warehouse_id IS NULL) AS null_warehouse_id,
    COUNT(*) FILTER (WHERE service_type IS NULL) AS null_service_type
FROM public.shipments;


-- Step 9: Check for duplicate shipment IDs.
-- This verifies that each loaded shipment has a unique identifier.

SELECT
    shipment_id,
    COUNT(*) AS duplicate_count
FROM public.shipments
GROUP BY shipment_id
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;


-- Step 10: Verify the distribution of shipment statuses.
-- This confirms how many loaded shipments are in each status.

SELECT
    status,
    COUNT(*) AS shipment_count
FROM public.shipments
GROUP BY status
ORDER BY shipment_count DESC;


-- Step 11: Verify numeric shipment values.
-- This checks for invalid or negative weight and shipping cost values.

SELECT
    COUNT(*) AS invalid_numeric_records
FROM public.shipments
WHERE weight_kg < 0
   OR shipping_cost < 0;


-- Step 12: Verify shipment and delivery date consistency.
-- This checks that delivery dates are not earlier than shipment dates.

SELECT
    shipment_id,
    shipment_date,
    delivery_date
FROM public.shipments
WHERE delivery_date IS NOT NULL
  AND delivery_date < shipment_date
ORDER BY shipment_id;


-- Step 13: Verify that no shipment has a negative weight.
-- This confirms that invalid negative-weight records were excluded
-- during validation before loading into PostgreSQL.

SELECT
    shipment_id,
    weight_kg
FROM public.shipments
WHERE weight_kg < 0;


-- Step 14: Verify that no shipment has a negative shipping cost.
-- This confirms that invalid negative shipping-cost records were
-- excluded during validation before loading into PostgreSQL.

SELECT
    shipment_id,
    shipping_cost
FROM public.shipments
WHERE shipping_cost < 0;


-- Step 15: Verify that each shipment has a unique shipment ID.
-- This confirms that duplicate shipment records were removed
-- before loading the valid data into PostgreSQL.

SELECT
    shipment_id,
    COUNT(*) AS occurrence_count
FROM public.shipments
GROUP BY shipment_id
HAVING COUNT(*) > 1
ORDER BY shipment_id;


-- Step 16: Perform a final record-count verification after the ETL reload.
-- This confirms that the expected 31 valid records are present
-- in the PostgreSQL shipments table.

SELECT
    COUNT(*) AS total_loaded_records
FROM public.shipments;


-- Step 17: Final verification of records loaded by the ETL pipeline.
-- This confirms the final number of records present in the shipments table.

SELECT COUNT(*) AS total_loaded_records
FROM public.shipments;