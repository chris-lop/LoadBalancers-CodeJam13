<template>
  <Container>
    <div class="grid grid-cols-2 surface-section text-white bg-gray-800">
      <!-- Left Section -->
      <div class="p-6 text-center md:text-left flex items-center">
        <section>
          <span class="text-orange-500 block text-5xl font-bold mb-1">LoadBalancer</span>
          <div class="text-5xl text-primary font-bold mb-3">helping truckers find their true match</div>
          <p class="mt-0 mb-4 text-700 line-height-3">
            Maximize your profits based on your interests!
          </p>

          <Button label="Login" type="button" class="mr-3 p-button-raised white-fill-button"></Button>
          <Button label="Register" type="button" class="p-button-outlined white-outline-button"></Button>
        </section>
      </div>

      <!-- Right Section -->
      <div>
        <img
        src="../assets/truck.jpg"
            alt="Image"
            style="clip-path: polygon(8% 0, 100% 0%, 100% 100%, 0 100%)"
          />
      </div>
    </div>

    <!-- Divider -->
    <!-- Features Section -->
    <div class="surface-section pt-8 md:px-6 lg:px-8 text-center bg-gray-900">
      <div class="mb-3 font-bold text-3xl">
        <span class="text-gray-300">One Product, </span>
        <span class="text-orange-500">Many Solutions</span>
      </div>
      <div class="grid md:grid-cols-3 gap-4">
        <!-- ... (rest of the code remains the same) ... -->
      </div>
    </div>

    <!-- Divider -->
    <!-- Feature Details -->
    <div class="surface-section py-8 md:px-6 lg:px-8 text-center bg-gray-900">
      <!-- Feature Details -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div class="mb-4 px-5">
          <!-- Feature Icon or Image -->
          <span class="p-3 shadow-lg mb-3 inline-block surface-card bg-primary rounded-lg" style="border-radius: 10px">
            <Button icon="pi pi-check" class="white-fill-button"></Button>
          </span>

          <!-- Feature Title -->
          <div class="text-900 text-xl mb-3 font-medium">Real time updates</div>

          <!-- Feature Description -->
        </div>

        <!-- Repeat the structure for other features -->
        <!-- ... (Add more features as needed) ... -->

        <!-- Feature Details 2 -->
        <div class="mb-4 px-5">
          <span class="p-3 shadow-lg mb-3 inline-block surface-card bg-primary rounded-lg" style="border-radius: 10px">
            <Button icon="pi pi-check" class="white-fill-button"></Button>
          </span>
          <div class="text-900 text-xl mb-3 font-medium">Personalised load matching</div>
        </div>

        <!-- Feature Details 3 -->
        <div class="mb-4 px-5">
          <span class="p-3 shadow-lg mb-3 inline-block surface-card bg-primary rounded-lg" style="border-radius: 10px">
            <Button icon="pi pi-check" class="white-fill-button"></Button>
          </span>
          <div class="text-900 text-xl mb-3 font-medium">Advanced technology integration</div>
        </div>
      </div>
    </div>
  </Container>
</template>

<style>
.white-fill-button {
  background-color: white;
  border-color: white; /* Set the border color to white */
  color: black; /* Set the text color to contrast with the white background */
}

.white-outline-button {
  border-color: white;
  color: white; /* Set the text color to match the outline color */
}
</style>
