export interface UserLogin {
  email: string;
  password: string;
}

export interface UserCreate extends UserLogin {
  username: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}
