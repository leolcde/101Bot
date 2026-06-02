from fastapi import HTTPException

from newsletter.schemas import NewsletterRequest

def create_newsletter(conn, data: NewsletterRequest):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT u.id, u.email
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_id = %s
            AND s.expires_at > NOW();
        """, (data.session_id,))

        user = cur.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired session")

        user_id = user[0]

        if data.frequency is None:
            data.frequency = "daily"
        if data.send_time is None:
            data.send_time = "8:00"
        if data.tone is None:
            data.tone = "neutral"
        if data.format is None:
            data.format = "short"
        if data.max_articles is None:
            data.max_articles = 5

        cur.execute("""
            INSERT INTO user_preferences (
                user_id,
                topics,
                frequency,
                send_time,
                tone,
                format,
                max_articles,
                is_subscribed,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, true, NOW())
            ON CONFLICT (user_id)
            DO UPDATE SET
                topics = EXCLUDED.topics,
                frequency = EXCLUDED.frequency,
                send_time = EXCLUDED.send_time,
                tone = EXCLUDED.tone,
                format = EXCLUDED.format,
                max_articles = EXCLUDED.max_articles,
                is_subscribed = true,
                updated_at = NOW()
            RETURNING id;
        """, (
            user_id,
            data.topics,
            data.frequency,
            data.send_time,
            data.tone,
            data.format,
            data.max_articles
        ))

        preference_id = cur.fetchone()[0]
        conn.commit()

        return {
            "success": True,
            "message": "Newsletter preferences saved✅",
            "preference_id": preference_id
        }