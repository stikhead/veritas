import mongoose from "mongoose";
import bcrypt from 'bcrypt';
import { v4 as uuid } from 'uuid';
import jwt from 'jsonwebtoken';

const userSchema = new mongoose.Schema({
    userID: {
        type: String,
        default: uuidv4,
        index: true,
        unique: true
    },

    userName: {
        type: String,
        default: "User",
        trim: true
    },

    email: {
        type: String,
        required: [true, "email is required"],
        trim: true,
        unique: true,
        lowercase: true,
        match: [/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
    },

    password: {
        type: String,
        required: [true, " password is required"],
        trim: true,
        minlength: 10,
        select: false
    },

    isVerfied: {
        type: Boolean,
        default: false,
        select: false
    },
    refreshToken: {
        type: String,
        select: false
    },

    verification: {
        emailToken: {
            type: string
        },

        emailTokenExpiry: {
            type: Date
        },

        passwordResetToken: {
            type: string
        },

        passwordResetToken: {
            type: Date
        },

        nextOtpAvailable: {
            type: Date
        },

        select: false
    }
}, {timestamp: true});


userSchema.pre("save", async function (next){
    if(this.isModified(password)){
        this.password = await bcrypt.hash(this.password, 10)
    }
});

userSchema.methods.generateAccessToken = async function () {
    return jwt.sign({
        _id: this._id,
        username: this.userName,
        email: this.email,
        check: this.isVerfied 
    }, process.env.ACCESS_TOKEN_SECRET, { expiresIn: process.env.ACCESS_TOKEN_EXPIRY})
}

userSchema.methods.generateRefreshToken = async function () {
    return jwt.sign({
        _id: this._id,
        check: this.isVerfied 
    }, process.env.REFRESH_TOKEN_SECRET, { expiresIn: process.env.REFRESH_TOKEN_EXPIRY})
}
export const UserSchema = mongoose.model("User", userSchema);