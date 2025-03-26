import { writable } from "svelte/store";
import { browser } from '$app/environment'



export const currentUser = writable( (browser && JSON.parse(localStorage.getItem("userData"))) ||{
  name: "",
  party: "",
  game: null
});


currentUser.subscribe((value) => {
  if(browser) {
    localStorage.setItem("userData", JSON.stringify(value));
  } 
});

export const setUserData = ({name, party, game}) => {
  currentUser.set({
    name: name || "",
    party: party || "",
    game: game || null,
  });
};

