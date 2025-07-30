# Exploring Basic React Native Components

Essential components for building React Native applications.

## Project Structure Recap

Before diving into components, let's review the basic React Native project structure:

```
/
├── .expo-shared/
├── assets/
├── node_modules/          # Dependencies (React, Expo, libraries)
├── .gitignore            # Files to exclude from version control
├── App.js                # Root component (entry point)
├── app.json              # App configuration
├── babel.config.js       # Babel configuration
├── package.json          # Project metadata & dependencies
└── yarn.lock             # Dependency lock file
```

### Key Files
- **`App.js`** - Your main component file where you'll use these basic components
- **`package.json`** - Manages all the component dependencies
- **`assets/`** - Store images and other static files for your components

## Core Components Overview

React Native provides fundamental building blocks similar to HTML elements but optimized for mobile development.

### 📦 `View` Component
**Purpose:** Container component for grouping other components
- Similar to `<div>` in HTML
- Supports flexbox layout, accessibility features
- Acts as a wrapper for organizing UI elements

```jsx
<View>
  {/* Other components go here */}
</View>
```

### 📝 `Text` Component
**Purpose:** Display text content
- Similar to `<p>` in HTML
- **Required** for all text in React Native (text cannot exist outside Text components)

```jsx
<Text>This is a text field</Text>
```

### 🔘 `Button` Component
**Purpose:** Generic button with press functionality
- Similar to `<button>` in HTML
- Requires `title` prop for button text
- Uses `onPress` event handler for interactions

```jsx
<Button
  title="Press me"
  onPress={() => Alert.alert('Simple Button pressed')}
/>
```

### 🚨 `Alert` Component
**Purpose:** Display system alerts
- Similar to JavaScript `alert()` function
- **Mobile-friendly** alternative to browser alerts
- Shows native alert dialogs

```jsx
// Triggered via Button onPress or other events
Alert.alert('Simple Button pressed')
```

> **💡 Tip:** Always use `Alert.alert()` instead of `alert()` on mobile devices

### 🖼️ `Image` Component
**Purpose:** Display images
- Similar to `<img>` in HTML
- Requires `source` prop with image path
- Supports local and remote images

```jsx
<Image
  source={require('./assets/favicon.png')}
/>
```

### 👆 `TouchableOpacity` Component
**Purpose:** Customizable touchable button
- More flexible than basic `Button` component
- Provides visual feedback (opacity change) on press
- Can contain any child components

```jsx
<TouchableOpacity onPress={() => Alert.alert('You tapped the button!')}>
  <Text>TouchableOpacity</Text>
</TouchableOpacity>
```

### ⌨️ `TextInput` Component
**Purpose:** Text input field for user data
- Similar to `<input>` in HTML
- Foundation for forms and user input
- Highly customizable with styling

```jsx
<TextInput
  style={styles.input}
  placeholder="Enter text here"
/>
```

## Component Hierarchy

```
App
├── View (container)
│   ├── Text (display text)
│   ├── Button (simple interactions)
│   ├── TouchableOpacity (custom buttons)
│   │   └── Text (button label)
│   ├── Image (media display)
│   └── TextInput (user input)
```

## Key Concepts

- **Container vs Content**: `View` groups components, `Text` displays content
- **Event Handling**: Use `onPress` for touch interactions
- **Mobile-First**: Components are designed for touch interfaces
- **Styling**: All components support custom styling via `style` prop
- **Accessibility**: Built-in accessibility features for better user experience

## Next Steps

These basic components form the foundation for more complex UI patterns. As you progress, you'll learn about:
- Props and State management
- Advanced layout techniques
- Navigation components
- Custom component creation

---

*Master these fundamentals before moving on to more advanced React Native concepts.*