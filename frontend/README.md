# Frontend

### Project Colors

???

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

### Chakra UI

[How to intall and config with vite](https://www.chakra-ui.com/docs/get-started/frameworks/vite)

How to [extend the theme conifg](https://www.chakra-ui.com/docs/theming/customization/overview)