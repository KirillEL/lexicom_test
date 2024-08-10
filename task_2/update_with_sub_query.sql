UPDATE full_names AS fn
SET status = (
    SELECT sn.status
    FROM short_names AS sn
    WHERE fn.name LIKE sn.name || '%'
    LIMIT 1
)
WHERE EXISTS (
    SELECT 1
    FROM short_names AS sn
    WHERE fn.name LIKE sn.name || '%'
);