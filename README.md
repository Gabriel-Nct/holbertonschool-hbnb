# 🏠 HBnB - Simple Web Client 🌐

Welcome to the HBnB Simple Web Client project! This front-end application connects with the back-end services developed in previous parts of the project.

## 🎯 Project Overview

This web client provides a user-friendly interface for interacting with the HBnB API. Built with HTML5, CSS3, and JavaScript ES6, it implements modern web development practices to create a dynamic web application.

## ✨ Features

-   🔐 **User Authentication**: Login functionality with JWT token storage
-   🏘️ **Place Listings**: Browse all available places with filtering options
-   📋 **Detailed Place Views**: View comprehensive information about individual places
-   ⭐ **Review System**: Authenticated users can leave reviews for places

## 💻 Pages

1.  **Login Page**: Secure authentication using the back-end API
2.  **Index Page**: Main listing of all places with filtering options
3.  **Place Details Page**: Comprehensive view of place information and reviews
4.  **Add Review Page**: Form for authenticated users to submit reviews

## 🛠️ Technologies Used

-   **HTML5** for semantic structure
-   **CSS3** for styling and responsive design
-   **JavaScript ES6** for client-side functionality
-   **Fetch API** for connecting with the back-end
-   **Cookie-based authentication** for session management

## 🚀 Getting Started

1.  Clone the repository
2.  Navigate to the `part4` directory
3.  Open the HTML files in your browser to explore the application

## 🔍 Implementation Details

### Task 0: Design

-   Customized HTML and CSS files following design specifications
-   Created responsive layouts for all required pages
-   Implemented semantic HTML5 structure for better accessibility

### Task 1: Login

-   Implemented form submission with Fetch API
-   Added JWT token storage in cookies
-   Included error handling for failed login attempts

### Task 2: Index

-   Fetched and displayed places data from the API
-   Implemented client-side filtering by price
-   Conditionally displayed UI elements based on authentication status

### Task 3: Place Details

-   Dynamically loaded place information using the place ID
-   Displayed comprehensive place details including amenities and reviews
-   Provided access to review form for authenticated users

### Task 4: Add Review

-   Created a form for submitting reviews
-   Implemented authentication checks with redirects
-   Added success/error messaging for form submission

## 📝 Notes

-   When testing against your API, you may encounter CORS errors. You'll need to modify your API to allow cross-origin requests.
-   All pages validate successfully with the W3C Validator.

## 🤝 Contributing

This project is part of a larger application. Feel free to explore the other parts in the holbertonschool-hbnb repository.

## ⚠️ CORS Configuration

When testing your client against your API, you'll likely encounter Cross-Origin Resource Sharing (CORS) errors. Make sure to configure your Flask API to allow cross-origin requests from your client.

## 📚 Resources

-   [HTML5 Documentation](https://developer.mozilla.org/en-US/docs/Web/HTML)
-   [CSS3 Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS)
-   [JavaScript ES6 Features](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
-   [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
-   [Handling Cookies in JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)

Happy coding! 🎉