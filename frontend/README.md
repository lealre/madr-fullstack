# Frontend

### Project Colors

[Pallete link](https://coolors.co/463f3a-8a817c-bcb8b1-f4f3ee-e0afa0)

- `#463f3a` - A dark brownish-gray, which is excellent for backgrounds, text, or as an accent.
- `#8a817c` - A soft taupe, ideal for secondary backgrounds or subtle elements.
- `#bcb8b1` - A light, warm gray that works well for secondary backgrounds or as a contrast to darker elements.
- `#f4f3ee` - A very light, almost white, beige, perfect for backgrounds or as a neutral space.
- `#e0afa0` - A warm, earthy light tan that can be used for highlights, buttons, or accents.

Backgrounds: Use `#f4f3ee` and `#bcb8b1` for page backgrounds or larger areas for a clean look.
Text: The darker color, `#463f3a`, would be effective for headers or main text.
Buttons/Accents: `#e0afa0` can be used for interactive elements like buttons or highlights to draw attention.
Borders and Dividers: `#8a817c` and #bcb8b1 would be suitable for subtle dividers or borders.

### Explanation of `useLocation()` in React Router

`useLocation()` is a hook provided by React Router that allows you to access the `location` object, which represents the current URL.
This `location` object contains properties like:

- **`pathname`**: The current path of the URL (e.g., `/dashboard`).
- **`search`**: Any query parameters in the URL (e.g., `?query=search`).
- **`hash`**: The anchor part of the URL (e.g., `#section1`).
- **`state`**: Custom state that can be passed via navigation, allowing data to be shared between routes (e.g., error messages or user data).

**Usage in this project**: To pass an error message to the login page if the user is not authenticated.

In `PrivateRoute.tsx`

```tsx
if (!token) {
  return (
    <Navigate to="/login" state={{ error: "You need to authenticate first" }} />
  );
}
```

The error message is passed as a `state` prop to `useLocation()`. It is rendered via `useEffect()` in `LoginPage.tsx`, stays visible for 5 seconds, and then is cleared.

```tsx
...
const location = useLocation();

useEffect(() => {
  if (location.state?.error) {
    setError(location.state.error);
  }

  navigate(location.pathname, { replace: true });

  const timer = setTimeout(() => {
    return setError("");
  }, 5000);

  return () => clearTimeout(timer);
}, [location.state]);
```
