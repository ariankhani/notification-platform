export interface User { id: number; username: string; email: string; name: string; last_name: string; created_at: string }
export interface TokenPair { access_token: string; refresh_token: string; token_type: 'bearer' }
export interface RegisterInput { username: string; email: string; name: string; last_name: string; password: string }
export interface ApiErrorPayload { detail?: string | Array<{ loc: Array<string | number>; msg: string; type: string }> }
