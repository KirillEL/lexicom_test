UPDATE full_names AS fn
SET status = sn.status
FROM short_names AS sn
JOIN full_names AS fn2 ON fn2.name LIKE sn.name || '%'
WHERE fn.id = fn2.id;

