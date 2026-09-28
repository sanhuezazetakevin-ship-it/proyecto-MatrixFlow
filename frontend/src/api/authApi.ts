import api from "./api";

import type {
  FacialLoginResponse,
  LoginResponse,
  User,
  FacialRegisterResponse
} from "../types/auth";


export async function loginWithPassword(
  email: string,
  password: string
): Promise<LoginResponse> {

  const formData = new URLSearchParams();

  formData.append(
    "username",
    email
  );

  formData.append(
    "password",
    password
  );

  const response =
    await api.post<LoginResponse>(
      "/api/auth/login",
      formData,
      {
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded",
        },
      }
    );

  return response.data;
}


export async function loginWithFace(
  dni: string,
  frames: Blob[]
): Promise<FacialLoginResponse> {

  if (frames.length !== 5) {
    throw new Error(
      "Se necesitan exactamente 5 capturas."
    );
  }

  const formData = new FormData();

  formData.append(
    "dni",
    dni
  );

  frames.forEach(
    (frame, index) => {

      formData.append(
        `frame${index + 1}`,
        frame,
        `frame${index + 1}.jpg`
      );

    }
  );

  const response =
    await api.post<FacialLoginResponse>(
      "/api/auth/login-facial-liveness",
      formData
    );

  return response.data;
}


export async function getCurrentUser():
Promise<User> {

  const response =
    await api.get<User>(
      "/api/auth/me"
    );

  return response.data;
}
export async function registerWithFace(
  dni: string,
  nombre: string,
  email: string,
  password: string,
  frames: Blob[]
): Promise<FacialRegisterResponse> {

  if (frames.length !== 3) {
    throw new Error(
      "Se necesitan exactamente 3 capturas faciales."
    );
  }

  const formData =
    new FormData();

  formData.append(
    "dni",
    dni
  );

  formData.append(
    "nombre",
    nombre
  );

  formData.append(
    "email",
    email
  );

  formData.append(
    "password",
    password
  );


  frames.forEach(
    (frame, index) => {

      formData.append(
        `frame${index + 1}`,
        frame,
        `frame${index + 1}.jpg`
      );

    }
  );


  const response =
    await api.post<FacialRegisterResponse>(
      "/api/auth/registro-facial",
      formData
    );


  return response.data;
}