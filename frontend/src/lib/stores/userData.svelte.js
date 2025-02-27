import { writable } from "svelte/store";

export const currentUser = writable({
  name: "",
  party: "",
});

export const setUserData = (name, party) => {
  currentUser.set({
    name: name || "",
    party: party || "",
  });
};

