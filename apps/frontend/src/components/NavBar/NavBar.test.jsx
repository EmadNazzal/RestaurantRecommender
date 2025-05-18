import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import NavBar from "./NavBar";

// Mock the CSS module
jest.mock("./navbar.module.css", () => ({
  navContainer: "navContainer",
  containerForLinks: "containerForLinks",
  signInBtn: "signInBtn",
}));

// Mock the logo image
jest.mock("../../assets/images/logopic.png", () => "logopic.png");

test("renders NavBar with links and sign in button", () => {
  const mockSignInClick = jest.fn();

  render(
    <BrowserRouter>
      <NavBar onSignInClick={mockSignInClick} />
    </BrowserRouter>
  );

  // Check for logo image
  const logoImage = screen.getByAltText("Logo Image");
  expect(logoImage).toBeInTheDocument();

  // Check for links
  expect(screen.getByText("Navigator")).toBeInTheDocument();
  expect(screen.getByText("About Us")).toBeInTheDocument();
  expect(screen.getByText("Contact Us")).toBeInTheDocument();

  // Check for sign in button
  const signInButton = screen.getByText("Sign In");
  expect(signInButton).toBeInTheDocument();

  // Check sign in button click
  fireEvent.click(signInButton);
  expect(mockSignInClick).toHaveBeenCalled();
});
