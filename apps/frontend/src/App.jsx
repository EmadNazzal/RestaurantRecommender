import { WelcomePage } from "./components/WelcomePage/WelcomePage";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import AboutUs from "./components/AboutUs/AboutUs";
import { ContactUs } from "./components/ContactUs/ContactUs";
import Dashboard from "./components/DashboardPage/Dashboard";
import ManageProfile from "./components/ManageProfile/ManageProfile";
import SignUp from "./components/SignUp/SignUp";
import SortedRestaurants from "./components/SortedRestaurants/SortedRestaurants";

// // Debugging: Print the value of VITE_CONFIGCAT_SDK_KEY
// console.log(import.meta.env);
// console.log(import.meta.env.VITE_CONFIGCAT_SDK_KEY);

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <WelcomePage />,
    },
    {
      path: "/aboutUs",
      element: <AboutUs />,
    },
    {
      path: "/contactUs",
      element: <ContactUs />,
    },
    {
      path: "/dashboard",
      element: <Dashboard />,
    },
    {
      path: "/manageaccount",
      element: <ManageProfile />,
    },
    {
      path: "/signup",
      element: <SignUp />,
    },
    {
      path: "/sorted-restaurants",
      element: <SortedRestaurants />,
    },
  ]);
  return (
    <>
      {/* <WelcomePage /> */}

      <RouterProvider router={router} />
    </>
  );
}

export default App;