<template>
  <div class="robot">
    <div class="head tilt">
      <span class="eye">^</span>
      <span class="mouth">v</span>
      <span class="eye">^</span>
    </div>

    <div class="limbs">
      <div class="arm"></div>
      <div class="body flex items-center justify-center p-2">
        <img src="../assets/zus.png" alt="ZUS logo" />
      </div>

      <!-- this one waves -->
      <div class="arm wave"></div>
    </div>

    <div class="legs">
      <div class="leg"></div>
      <div class="leg"></div>
    </div>
  </div>
</template>

<style scoped>
.robot {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: monospace;

  & > * {
      filter: drop-shadow(0px 0px 0px 2px);
  }
}

.head {
  background-color: black;
  border-color: #1e8f4e;
  border-width: 24px 12px;
  width: 140px;
  height: 120px;
  border-radius: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  transform-origin: center bottom;
  z-index: 1;
}

span {
    opacity: .5;
}

.eye, .mouth {
  font-size: 32px;
  color: #1e8f4e;
  font-weight: bold;
  margin: 0 8px;
}

.eye {
  align-self: flex-start;
}

.mouth {
  align-self: flex-end;
}

.body {
  background: #1e8f4e;
  width: 50px;
  height: 48px;
  border-radius: 16px;
  margin: 4px;
}

.limbs, .legs {
  display: flex;
  margin-top: 4px;
}

.legs {
  gap: 8px;
}

.arm, .leg {
  background: #1e8f4e;
  width: 18px;
  height: 64px;
  border-radius: 8px;
}

.arm {
  transform-origin: center top; /* pivot for nicer waving */
}

.tilt {
  animation: tilt 2.5s ease-in-out infinite;
}

@keyframes tilt {
  0%    { transform: rotate(0deg); }
  30%   { transform: rotate(-8deg); }
  35%   { transform: rotate(-16deg); }
  70%   { transform: rotate(-16deg); }
  80%   { transform: rotate(0deg); }
  100%  { transform: rotate(0deg); }
}

/* waving animation */
.wave {
    position: relative;
  z-index: 2;
  animation: chirp-wave 2.5s cubic-bezier(.3, .6, .5, 1.4) infinite;
}

@keyframes chirp-wave {
  0%   { transform: rotate(0deg); }
  30%  { transform: rotate(-135deg); }   /* quick flick */
  35%  { transform: rotate(-108deg); }   /* tiny recoil */
  40%  { transform: rotate(-128deg); }   /* flick again */
  45%  { transform: rotate(-108deg); }   /* tiny recoil */
  50%  { transform: rotate(-125deg); }   /* flick again */
  55%  { transform: rotate(-108deg); }   /* tiny recoil */
  60%  { transform: rotate(-128deg); }   /* flick again */
  70%  { transform: rotate(-108deg); }   /* tiny recoil */
  80%  { transform: rotate(-0deg); }      /* reset */
}

span {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
