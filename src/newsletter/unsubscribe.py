from fastapi import HTTPException, Body

def unsubscribe(conn, session_id: str):
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
            UPDATE user_preferences
            SET is_subscribed = false, updated_at = NOW()
            WHERE user_id = %s
            RETURNING *
        """,(user_id,))

        result = cur.fetchone()
        conn.commit()
        return {
            "success": True,
            "message": "Successfully unsubcribed from newsletter✅",
            "data": result
        }