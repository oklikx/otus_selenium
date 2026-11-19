# src/lib/db.py l
import hashlib
from typing import Optional

TABLE_PREFIX = "ps_"


def create_customer(connection, customer_data: dict) -> int:
    secure_key = hashlib.md5(customer_data['email'].encode()).hexdigest()
    sql = f"""
        INSERT INTO {TABLE_PREFIX}customer
        (id_shop_group, id_shop, id_gender, id_default_group, id_lang,
         firstname, lastname, email, passwd, secure_key,
         active, newsletter, optin, date_add, date_upd)
        VALUES (1, 1, %s, 1, 1,
                %s, %s, %s, %s, %s,
                1, 0, 0, NOW(), NOW())
    """
    values = (
        customer_data.get('id_gender', 1),
        customer_data['firstname'],
        customer_data['lastname'],
        customer_data['email'],
        customer_data.get('passwd', 'test_password'),
        secure_key,
    )
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
        connection.commit()
        return cursor.lastrowid


def get_customer_by_id(connection, customer_id: int) -> Optional[dict]:
    sql = f"SELECT * FROM {TABLE_PREFIX}customer WHERE id_customer = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, (customer_id,))
        return cursor.fetchone()


def update_customer(connection, customer_id: int, update_data: dict) -> int:
    fields = [f"{k} = %s" for k in update_data]
    values = list(update_data.values())
    if not fields:
        return 0
    sql = f"UPDATE {TABLE_PREFIX}customer SET {', '.join(fields)} WHERE id_customer = %s"
    values.append(customer_id)
    with connection.cursor() as cursor:
        affected = cursor.execute(sql, values)
        connection.commit()
        return affected


def delete_customer(connection, customer_id: int) -> int:
    sql = f"DELETE FROM {TABLE_PREFIX}customer WHERE id_customer = %s"
    with connection.cursor() as cursor:
        affected = cursor.execute(sql, (customer_id,))
        connection.commit()
        return affected
