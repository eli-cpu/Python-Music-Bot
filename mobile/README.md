# Spotify Wrapper Mobile App

React Native mobile application for the Spotify Wrapper platform.

## Features

- 🎵 Search for music on Spotify
- 🔍 Browse and view playlists
- 📱 Native iOS and Android experience
- 🎨 Modern, Spotify-inspired UI
- 🔐 Spotify OAuth authentication

## Prerequisites

- Node.js 16+
- React Native development environment set up
  - For iOS: Xcode 12+
  - For Android: Android Studio with SDK
- CocoaPods (for iOS)

## Installation

```bash
npm install
```

### iOS Setup

```bash
cd ios
pod install
cd ..
```

### Android Setup

No additional setup required. Make sure Android SDK is installed via Android Studio.

## Configuration

Create a `.env` file in the mobile directory:

```env
REACT_APP_API_URL=https://your-api-domain.com/api
```

For local development, the app defaults to `http://localhost:5000/api` if no environment variable is set.

## Running the App

### iOS

```bash
npm run ios
```

Or open `ios/SpotifyWrapperMobile.xcworkspace` in Xcode and run from there.

### Android

```bash
npm run android
```

Or open the `android` folder in Android Studio and run from there.

## Project Structure

```
mobile/
├── src/
│   ├── screens/         # App screens
│   │   ├── LoginScreen.js
│   │   ├── HomeScreen.js
│   │   ├── SearchScreen.js
│   │   └── PlayerScreen.js
│   └── services/        # API integration
│       └── ApiService.js
├── App.js              # Main app component
└── package.json        # Dependencies
```

## Screens

### LoginScreen
- Spotify OAuth login flow
- Clean, welcoming interface

### HomeScreen
- Dashboard with feature highlights
- Quick navigation to other screens
- Feature overview

### SearchScreen
- Real-time music search
- Track listing with album art
- Direct playback integration

### PlayerScreen
- Now playing display
- Track information and album art
- Playback controls (integration in progress)

## Known Limitations

### Audio Playback
The current implementation logs stream URLs but doesn't play audio directly. To add full audio playback:

1. Install `react-native-track-player`:
   ```bash
   npm install react-native-track-player
   ```

2. Update `PlayerScreen.js` to integrate the track player

3. Handle playback state, progress, and controls

See [react-native-track-player documentation](https://github.com/doublesymmetry/react-native-track-player) for details.

## React Native Version

Currently using React Native 0.72.0. Consider upgrading to 0.74.x or later for:
- Performance improvements
- Bug fixes
- Security patches
- New features

To upgrade:
```bash
npx react-native upgrade
```

## API Integration

The app communicates with the backend API through `ApiService.js`. All API calls are configured to:
- Use environment-based URLs
- Handle authentication tokens
- Manage session state with AsyncStorage

## Troubleshooting

### iOS Build Issues
- Clean build folder: `cd ios && xcodebuild clean && cd ..`
- Reinstall pods: `cd ios && pod install && cd ..`
- Clear cache: `npm start -- --reset-cache`

### Android Build Issues
- Clean build: `cd android && ./gradlew clean && cd ..`
- Clear cache: `npm start -- --reset-cache`
- Check SDK versions in `android/build.gradle`

### API Connection Issues
- Verify backend is running
- Check `REACT_APP_API_URL` in `.env`
- For local development on device, use computer's IP address instead of localhost
- Ensure CORS is properly configured in backend

## Development Tips

### Running on Physical Device

For iOS:
1. Connect device via USB
2. Select device in Xcode
3. Run build

For Android:
1. Enable USB debugging on device
2. Connect via USB
3. Run `npm run android`

### Hot Reload

React Native supports fast refresh. Changes to code will automatically reload in the app.

### Debugging

- Use React Native Debugger or Chrome DevTools
- Access developer menu:
  - iOS: Cmd+D (simulator) or shake device
  - Android: Cmd+M (emulator) or shake device

## Contributing

When adding new features:
1. Follow existing code structure
2. Update this README with new screens/features
3. Test on both iOS and Android
4. Ensure API integration works correctly

## License

See main project LICENSE file.
