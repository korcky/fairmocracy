import { writable } from "svelte/store";
import { browser } from '$app/environment'



export const currentUser = writable( (browser && JSON.parse(localStorage.getItem("userData"))) ||{
  name: "",
  game: null,
  userId: null,
  affiliations: [],
  rounds: []
});


currentUser.subscribe((value) => {
  if(browser) {
    localStorage.setItem("userData", JSON.stringify(value));
  } 
});

export const setUserData = ({name, game, userId, affiliations, rounds}) => {
  currentUser.set({
    name: name || "",
    game: game || null,
    userId: userId || null,
    affiliations: affiliations || [],
    rounds: rounds || []

  });
};

