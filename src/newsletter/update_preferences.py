from fastapi import HTTPException

from newsletter.schemas import NewsletterRequest


def apply_topics_action(current_topics, new_topics, action):
    current_topics = current_topics or []
    new_topics = new_topics or []

    if action == "replace":
        return new_topics

    if action == "add":
        return list(dict.fromkeys(current_topics + new_topics))

    if action == "remove":
        return [
            topic for topic in current_topics
            if topic not in new_topics
        ]

    return current_topics


def update_preferences(conn, data: NewsletterRequest):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT u.id, up.topics
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            LEFT JOIN user_preferences up ON up.user_id = u.id
            WHERE s.session_id = %s
            AND s.expires_at > NOW()
        """, (data.session_id,))

        user = cur.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid session")

        user_id = user[0]
        current_topics = user[1] or []

        updates = []
        values = []

        if data.topics is not None and data.topics_action is not None:
            final_topics = apply_topics_action(
                current_topics,
                data.topics,
                data.topics_action
            )
            updates.append("topics = %s")
            values.append(final_topics)

        if data.frequency is not None:
            updates.append("frequency = %s")
            values.append(data.frequency)

        if data.send_day is not None:
            updates.append("send_day = %s")
            values.append(data.send_day)

        if data.send_day_of_month is not None:
            updates.append("send_day_of_month = %s")
            values.append(data.send_day_of_month)

        if data.send_time is not None:
            updates.append("send_time = %s")
            values.append(data.send_time)

        if data.tone is not None:
            updates.append("tone = %s")
            values.append(data.tone)

        if data.length is not None:
            updates.append("length = %s")
            values.append(data.length)

        if data.format is not None:
            updates.append("format = %s")
            values.append(data.format)

        if data.max_articles is not None:
            updates.append("max_articles = %s")
            values.append(data.max_articles)
        

        if not updates:
            return {"success": False, "message": "No fields to update"}

        updates.append("updated_at = NOW()")
        values.append(user_id)

        query = f"""
            UPDATE user_preferences
            SET {", ".join(updates)}
            WHERE user_id = %s
            RETURNING *
        """

        cur.execute(query, values)
        result = cur.fetchone()
        conn.commit()

        return {
            "success": True,
            "message": "Newsletter preferences updated✅",
            "data": result
        }