import { source } from "sveltekit-sse";
// import { SSE_API_KEY } from "$env/static/private";

export function createSSEConnection(endpoint, options = {}) {
  const defaultOptions = {
    options: {
      headers: {
        // "X-API-Key": SSE_API_KEY,
      },
    },
    // Other default configuration here
  };

  const config = {
    ...defaultOptions,
    ...options,
    options: {
      ...defaultOptions.options,
      ...options.options,
      headers: {
        ...defaultOptions.options.headers,
        ...(options.options?.headers || {}),
      },
    },
  };

  return source(endpoint, config);
}

export function selectJsonEvent(connection, eventName = "message") {
  return connection.select(eventName).json(({ error, raw }) => {
    if (error) {
      console.error("Failed to parse JSON:", raw, error);
      return false;
    }
    console.log("Received JSON event:", eventName, raw);
    return raw;
  });
}
