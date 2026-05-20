/*
** Project  -  persona
** Date     -  May 18, 2026
**
** Copyright (c) 2026 Léo Lacordaire
*/

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS auth_tokens (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  token VARCHAR(255) NOT NULL,
  type VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  session_ref VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS session_state (
  session_id VARCHAR(255) PRIMARY KEY,
  state VARCHAR(50) DEFAULT 'idle',
  email VARCHAR(255),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_auth_tokens_email ON auth_tokens(email);
CREATE INDEX IF NOT EXISTS idx_auth_tokens_session_ref ON auth_tokens(session_ref);
CREATE INDEX IF NOT EXISTS idx_session_state_email ON session_state(email);