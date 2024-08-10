let title = document.querySelector('.random');  // Select the element with the class 'random'
let randomNumber = Math.floor(Math.random() * 10) + 1;  // Generate a random number between 1 and 10
title.textContent = randomNumber;  // Set the text content of the selected element to the random number
