# What are Props? (Super Simple Explanation)

## Think of Props like Information You Give to Someone

Imagine you ask your friend to **"make a sandwich"**. But you need to tell them:
- What bread? (white, brown, etc.)
- What filling? (cheese, ham, etc.)
- How many? (1, 2, 3, etc.)

**Props are the information you give to a component!**

## Real Life Example: Instagram Profile

When Instagram shows a profile, it needs information:
- **What photo** to show?
- **What username** to display?
- **How many followers** to show?

```jsx
// This is like telling Instagram: "Show John's profile"
<ProfileCard 
  photo="john-photo.jpg"
  username="john_doe" 
  followers={1500}
/>
```

The `photo`, `username`, and `followers` are **PROPS** (information given to the component).

## Simple Component Example

```jsx
// This component needs information to work
const UserCard = (props) => {
  return (
    <View>
      <Image source={{uri: props.photo}} />
      <Text>{props.name}</Text>
      <Text>{props.age} years old</Text>
    </View>
  )
}

// Using the component with different information (props)
<UserCard photo="john.jpg" name="John" age={25} />
<UserCard photo="jane.jpg" name="Jane" age={30} />
<UserCard photo="bob.jpg" name="Bob" age={22} />
```

Same component, different information = different results!

## WhatsApp Example

When WhatsApp shows a chat message:

```jsx
const ChatMessage = (props) => {
  return (
    <View>
      <Text>{props.sender}: {props.message}</Text>
      <Text>{props.time}</Text>
    </View>
  )
}

// Different messages using the same component
<ChatMessage sender="Mom" message="Don't forget dinner!" time="2:30 PM" />
<ChatMessage sender="John" message="See you tomorrow" time="3:45 PM" />
<ChatMessage sender="Boss" message="Meeting at 10 AM" time="9:15 AM" />
```

## Props = Like a Form You Fill Out

Think of props like filling out a form:

**Netflix Movie Card Form:**
- Movie Title: ________________
- Movie Poster: ________________
- Rating: ________________
- Year: ________________

```jsx
const MovieCard = (props) => {
  return (
    <View>
      <Image source={{uri: props.poster}} />
      <Text>{props.title}</Text>
      <Text>⭐ {props.rating}</Text>
      <Text>{props.year}</Text>
    </View>
  )
}

// Filling out the "form" with different movies
<MovieCard title="Avengers" poster="avengers.jpg" rating={4.5} year={2019} />
<MovieCard title="Titanic" poster="titanic.jpg" rating={4.8} year={1997} />
```

## Restaurant Menu Analogy 🍔

Imagine a restaurant has a **"Burger Recipe"** (component):

```jsx
const Burger = (props) => {
  return (
    <View>
      <Text>Burger with {props.meat}</Text>
      <Text>Bun: {props.bun}</Text>
      <Text>Price: ${props.price}</Text>
      <Text>Extras: {props.extras}</Text>
    </View>
  )
}

// Same recipe, different ingredients (props)
<Burger meat="beef" bun="sesame" price={8} extras="cheese, lettuce" />
<Burger meat="chicken" bun="wheat" price={7} extras="mayo, tomato" />
<Burger meat="veggie" bun="plain" price={6} extras="avocado" />
```

Same burger component, but each burger is different because of the **props** (ingredients you specified)!

## Key Points:

1. **Props = Information** you give to a component
2. **Same component** can show different things with different props
3. **Props are like filling out a form** with specific details
4. **You can't change props** inside the component (they're given from outside)

## Visual Example:

```
YouTube Video Component:

Props needed:
├── video title
├── video thumbnail  
├── channel name
├── view count
├── upload date

Result: One video card showing all this information
```

## In Super Simple Terms:

**Props** = The details you give to a component so it knows what to show

Just like:
- Telling a painter **what to paint** (props) → they paint it (component)
- Telling a chef **what ingredients to use** (props) → they cook it (component)  
- Telling Instagram **whose profile to show** (props) → it displays it (component)

**That's it! Props are just the information components need to do their job! 📝**