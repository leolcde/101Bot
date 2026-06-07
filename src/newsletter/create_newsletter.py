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

        topics = data.topics or []
        frequency = data.frequency or "daily"
        send_day = data.send_day or "monday"
        send_day_of_month = data.send_day_of_month or "1"
        send_time = data.send_time or "08:00"
        tone = data.tone or "neutral"
        length = data.length or "detailed"
        format_value = data.format
        max_articles = data.max_articles or 5

        cur.execute("""
            INSERT INTO user_preferences (
                user_id,
                topics,
                frequency,
                send_day,
                send_day_of_month,
                send_time,
                tone,
                length,
                format,
                max_articles,
                is_subscribed,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true, NOW())
            ON CONFLICT (user_id)
            DO UPDATE SET
                topics = EXCLUDED.topics,
                frequency = EXCLUDED.frequency,
                send_day = EXCLUDED.send_day,
                send_day_of_month = EXCLUDED.send_day_of_month,
                send_time = EXCLUDED.send_time,
                tone = EXCLUDED.tone,
                length = EXCLUDED.length,
                format = EXCLUDED.format,
                max_articles = EXCLUDED.max_articles,
                is_subscribed = true,
                updated_at = NOW()
            RETURNING id;
        """, (
            user_id,
            topics,
            frequency,
            send_day,
            send_day_of_month,
            send_time,
            tone,
            length,
            format_value,
            max_articles
        ))

        preference_id = cur.fetchone()[0]
        conn.commit()

        return {
            "success": True,
            "message": "Newsletter preferences saved ✅",
            "preference_id": preference_id
        }