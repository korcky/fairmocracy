import { source } from "sveltekit-sse";
// import { SSE_API_KEY } from "$env/static/private";

export function createSSEConnection(endpoint, options = {}) {
  const defaultOptions = {
    options: {
      method: "GET",
      headers: {
        // "X-API-Key": SSE_API_KEY,
      },
    },
    // Other default configuration here
  };

  const config = {
    close({ connect }) {
      console.log('reconnecting...')
      connect()
    },

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
  return connection.select(eventName).json(({ error, raw, previous }) => {
    console.log("huhhu")
    if (error) {
      console.error("Failed to parse JSON:", raw, error);
      console.log(raw)
      return previous;
    }
    console.log("Received JSON event:", eventName, raw);
    return raw;
  });
}
