# Django E-commerce Project

This project is a simple e-commerce web application built with Django, featuring product and category displays, and a shopping cart.

## Features

- **Home Page**: Displays categories and products.
- **Product Detail Page**: Shows detailed information about specific products.
- **Cart Functionality**: Users can add, update, and remove items in their cart.

## Project Structure

The project includes the following apps:

- **store**: Contains models, views, and templates for products and categories.
- **order**: Manages cart-related functionalities (add, update, remove items).
- **users**: Handles user authentication and management.

### Order App Views

#### `add_to_cart(request, product_id)`
- Adds a product to the user's cart if it's in stock. If the product is out of stock, an error message is displayed.

#### `view_cart(request)`
- Displays the items in the user's cart, calculating the total price for each item and the overall count.

#### `update_cart_item(request, item_id)`
- Updates the quantity of a specific cart item, ensuring the requested quantity does not exceed available stock. If the quantity is invalid, an error message is shown.

#### `remove_from_cart(request, item_id)`
- Removes a specified item from the cart.

#### `checkout(request)`
- Renders the checkout page.

### Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the server: `python manage.py runserver`.
