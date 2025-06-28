# Chess Coach - Web Application

This is the frontend web application for the Chess Coach platform, built with React, TypeScript, and Material-UI.

## Features

- Interactive chess board with move validation
- Real-time chat with AI chess coach
- Game analysis and position evaluation
- Tactics training and puzzles
- Personalized training plans
- Game database and history
- Responsive design for desktop and mobile

## Prerequisites

- Node.js (v14 or later)
- npm or yarn
- Backend API server (see main project README)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chess-coach.git
   cd chess-coach/web
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Create a `.env` file in the web directory with the following variables:
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

## Available Scripts

In the project directory, you can run:

### `npm start` or `yarn start`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test` or `yarn test`

Launches the test runner in interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build` or `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

## Project Structure

```
src/
  components/     # Reusable UI components
  pages/          # Page components
  services/       # API and service layer
  styles/         # Global styles and themes
  utils/          # Utility functions
  hooks/          # Custom React hooks
  context/        # React context providers
  types/          # TypeScript type definitions
  App.tsx         # Main application component
  index.tsx       # Application entry point
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Chess.js](https://github.com/jhlywa/chess.js) - Chess move validation
- [React Chessboard](https://github.com/Clariity/react-chessboard) - Interactive chess board
- [Material-UI](https://material-ui.com/) - React UI components
- [React Router](https://reactrouter.com/) - Client-side routing
