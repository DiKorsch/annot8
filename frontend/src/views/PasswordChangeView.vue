<template>
    <v-container fluid>
        <v-card v-if="loggedIn">
            <v-card-title>
                Changing Password for {{ username }}
            </v-card-title>
            <v-card-text>
                Please enter your old password and new password to change your password.
                <v-row>
                    <v-col cols="12">
                        <v-form ref="form" @submit.prevent="changePassword">
                            <v-text-field
                                v-model="oldPassword"
                                :rules="oldPasswordRules"
                                label="Old Password"
                                type="password"
                            ></v-text-field>
                            <v-text-field
                                v-model="newPassword"
                                :rules="newPasswordRules"
                                label="New Password"
                                type="password"
                            ></v-text-field>
                            <v-text-field
                                v-model="confirmPassword"
                                :rules="confirmPasswordRules"
                                label="Confirm Password"
                                type="password"
                            ></v-text-field>
                            <v-btn type="submit" color="primary">Change Password</v-btn>
                        </v-form>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {
            oldPassword: "",
            newPassword: "",
            confirmPassword: "",
            oldPasswordRules: [
                (v) => !!v || "Old Password is required",
            ],
            newPasswordRules: [
                (v) => !!v || "New Password is required",
                (v) => (v && v.length >= 8) || "Password must be at least 8 characters",
            ],
            confirmPasswordRules: [
                (v) => !!v || "Confirm Password is required",
                (v) => v === this.newPassword || "Passwords do not match",
            ],
        };
    },

    computed: {
        ...mapGetters("auth", ["loggedIn", "username"]),
    },
    methods: {
        changePassword() {
            if (this.$refs.form.validate()) {
                this.$store.dispatch("auth/changePassword", {
                    oldPassword: this.oldPassword,
                    newPassword: this.newPassword,
                }).then(
                    () => {
                        this.$router.push({ name: "index" });
                    },
                    err => {
                        console.error(err);
                    }
                );
            }
        },
    },
};
</script>
