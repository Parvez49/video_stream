# Use Node.js for development environment
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the project
COPY . .

# Expose the development server port
EXPOSE 3000

# Start the React development server with hot reloading
CMD ["npm", "start"]
