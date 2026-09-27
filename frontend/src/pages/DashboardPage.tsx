import { useNavigate }
  from "react-router-dom";

import { useAuth }
  from "../context/AuthContext";


export default function DashboardPage() {

  const navigate =
    useNavigate();

  const {
    user,
    logout,
  } = useAuth();


  function handleLogout() {

    logout();

    navigate(
      "/login",
      {
        replace: true,
      }
    );
  }


  return (
    <main className="dashboard-page">

      <div className="dashboard-card">

        <p className="eyebrow">
          MATRIXFLOW
        </p>

        <h1>
          Bienvenido, {user?.nombre}
        </h1>

        <p>
          Tu autenticación funciona
          correctamente.
        </p>


        <div className="user-data">

          <div>
            <span>Correo</span>
            <strong>
              {user?.email}
            </strong>
          </div>

          <div>
            <span>Rol</span>
            <strong>
              {user?.rol}
            </strong>
          </div>

        </div>


        <button
          className="secondary-button"
          onClick={handleLogout}
        >
          Cerrar sesión
        </button>

      </div>

    </main>
  );
}