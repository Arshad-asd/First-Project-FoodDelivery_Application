select * 
from users_product, users_productsize, users_category
;

-- @block
select 
    p."Product_name" as product_name,
    p.description as description,
    ps.size as size,
    ps.price as price,
    ps."Quantity" as quantity,
    c.categoryes as category_name,
    p."Product_Image" as product_image
from users_product as p
inner join users_productsize as ps
on p.id = ps.product_id
inner join users_category as c
on p.category_id = c.id
;

-- @block
select 
    p."Product_name"
from users_product as p
inner join users_productsize as ps
on p.id = ps.product_id
inner join users_category as c
on p.category_id = c.id
;

