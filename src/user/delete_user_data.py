from fastapi import HTTPException

def delete_user_data(conn, session_id: str):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT u.id
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_id = %s
            AND s.expires_at > NOW()
        """, (session_id,))

        user = cur.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid session")

        user_id = user[0]

        cur.execute("""
            DELETE FROM users
            WHERE id = %s
            RETURNING id
        """, (user_id,))

        deleted_user = cur.fetchone()

        if not deleted_user:
            conn.rollback()
            raise HTTPException(status_code=404, detail="User not deleted")

        conn.commit()

        return {
            "success": True,
            "message": "Successfully deleted all your data ✅",
            "deleted_user_id": deleted_user[0]
        }