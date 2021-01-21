setTimeout(() => {
  console.log("500ms one");
}, 500);

setTimeout(() => {
  console.log("1500ms one");
}, 1500);

setTimeout(() => {
  console.log("1000ms one");
}, 1000);

state = { resolved: false };
currentTime = Date.now();

const runSetTimeoutsAfter = (ms) => {
  while (!state.resolved)
    new Promise((r) => {
      if (Date.now() - currentTime >= ms) state.resolved = true;
      r();
    });
};

runSetTimeoutsAfter(2000);
