# Django E-commerce Project

This project is a simple e-commerce web application built with Django. It includes features for displaying products, categories, and a contact page.

## Features

- **Home Page**: Displays parent categories, fruits, and vegetables products.
- **Category List Page**: Lists products in a specific category or displays all products if no category is specified.
- **Product Detail Page**: Shows detailed information about a specific product.
- **Contact Page**: A simple contact form page.

## Project Structure

The project includes the following apps:

- **store**: Contains models, views, and templates related to products and categories.
- **order**: Manages the order-related functionalities (not detailed here).
- **users**: Handles user authentication, cart management, and user-related functionalities.

### Models

- **Product**: Represents the product details.
- **Category**: Represents the categories under which products are listed.
- **Cart**: Manages the user's shopping cart.
- **CartItem**: Represents items within the user's cart.
- **User**: Custom user model with signals for account management.

