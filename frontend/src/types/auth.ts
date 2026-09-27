export interface User {
  id: number;
  nombre: string;
  email: string;
  rol: string;
  activo: boolean;
  created_at?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  success: boolean;
  mensaje: string;
  usuario: User;
}

export interface FacialBiometrics {
  similitud: number;
  umbral: number;
  pose_change: number;
  detection_score: number;
  face_ratio: number;
}

export interface FacialLoginResponse
  extends LoginResponse {
  biometria: FacialBiometrics;
}
export interface FacialRegisterResponse
  extends LoginResponse {

  persona: {
    id: number;
    dni: string;
    nombre: string;
    email: string;
  };

  biometria: {
    embeddings_registrados: number;
  };
}