function logoutFirebase() {
    firebase.auth().signOut().then(function() {
      // Sign-out successful.
    }, function(error) {
      alert(error)
    });
  }
  
  var firebaseuiAuthContainer = document.getElementById("firebaseui-auth-container");
  var userAuthContainer = document.getElementById("user-auth-container");
  var userNameContainer = document.getElementById("userNameContainer");
  var mainContainer = document.getElementById("main");


  document.addEventListener('DOMContentLoaded', function() {
    // // 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    // // The Firebase SDK is initialized and available here!
    //


    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        firebaseuiAuthContainer.style.display = "none";
        userAuthContainer.style.display = "block";
        main.style.display = 'block';
        userNameContainer.innerText = user.email
      } else {
        firebaseuiAuthContainer.style.display = "block";
        userAuthContainer.style.display = "none";
        main.style.display = 'none';
      }
    });

    // firebase.database().ref('/path/to/ref').on('value', snapshot => { });
    // firebase.messaging().requestPermission().then(() => { });
    // firebase.storage().ref('/path/to/ref').getDownloadURL().then(() => { });
    //
    // // 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥

    try {
      let app = firebase.app();
      let features = ['auth', 'database', 'messaging', 'storage'].filter(feature => typeof app[feature] === 'function');
      document.getElementById('load').innerHTML = `Firebase SDK loaded with ${features.join(', ')}`;
    } catch (e) {
      console.error(e);
      document.getElementById('load').innerHTML = 'Error loading the Firebase SDK, check the console.';
    }

// Initialize the FirebaseUI Widget using Firebase.
var ui = new firebaseui.auth.AuthUI(firebase.auth());

var uiConfig = {
callbacks: {
signInSuccessWithAuthResult: function(authResult, redirectUrl) {
  // User successfully signed in.
  // Return type determines whether we continue the redirect automatically
  // or whether we leave that to developer to handle.
  return true;
},
uiShown: function() {
  // The widget is rendered.
  // Hide the loader.
  document.getElementById('loader').style.display = 'none';
}
},
// Will use popup for IDP Providers sign-in flow instead of the default, redirect.
signInFlow: 'popup',
signInSuccessUrl: window.location.href,
  signInOptions: [
      {
        provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
          signInMethod: firebase.auth.EmailAuthProvider.EMAIL_LINK_SIGN_IN_METHOD
          },
    {
  provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
  scopes: [],
  customParameters: {
    // Forces account selection even when one account
    // is available.
    prompt: 'select_account'
  }
},],
    };
ui.start('#firebaseui-auth-container', uiConfig)

});