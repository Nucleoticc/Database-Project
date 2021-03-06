<template>
  <form @submit.prevent="submitForm">
    <div class="field">
      <label class="label">Email</label>
      <div class="control">
        <input
          :class="{ input: email.isValid, 'input is-danger': !email.isValid }"
          type="email"
          placeholder="john_smith@example.com"
          v-model.trim="email.val"
          @blur="clearValidity('email')"
        />
      </div>
      <p v-if="!email.isValid" class="help is-danger">This Field is required</p>
    </div>
    <div class="field">
      <label class="label">Password</label>
      <div class="control">
        <input
          :class="{
            input: password.isValid,
            'input is-danger': !password.isValid,
          }"
          v-model.trim="password.val"
          type="password"
          @blur="clearValidity('password')"
        />
      </div>
      <p v-if="!password.isValid" class="help is-danger">
        This Field is required
      </p>
    </div>
    <div class="field">
      <div class="control">
        <button class="button">Login</button>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  emits: ["save-data"],
  data() {
    return {
      email: {
        val: "",
        isValid: true,
      },
      password: {
        val: "",
        isValid: true,
      },
      formIsValid: true,
    };
  },
  methods: {
    clearValidity(input) {
      this[input].isValid = true;
    },
    validateForm() {
      this.formIsValid = true;
      if (this.email.val === "") {
        this.email.isValid = false;
        this.formIsValid = false;
      }
      if (this.password.val === "") {
        this.password.isValid = false;
        this.formIsValid = false;
      }
    },
    submitForm() {
      this.validateForm();
      if (!this.formIsValid) {
        return;
      }
      const formData = {
        email: this.email.val,
        password: this.password.val,
      };
      this.$router.replace('/student')
      this.$emit("save-data", formData);
    },
  },
};
</script>

<style scoped></style>
