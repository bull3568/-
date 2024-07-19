login = """
    select 
    * 
    from 
    `user_info`
    where 
    `id` = %s and `password` = %s
"""

company = """
    select 
    * 
    from 
    `company_info`
"""

history = """
    insert into 
    `user_history`(`id`, `company_name`, `selected`)
    values (%s, %s, %s)
"""