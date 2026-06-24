import mongoose from "mongoose";
import bcrypt from 'bcrypt';
import { v4 as uuidv4  } from 'uuid';
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

    isVerified: {
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
            type: String
        },

        emailTokenExpiry: {
            type: Date
        },

        passwordResetToken: {
            type: String
        },

        passwordResetTokenExpiry: {
            type: Date
        },

        nextOtpAvailable: {
            type: Date
        },

        select: false
    }
}, {timestamps: true});


userSchema.pre("save", async function (next){
    if(this.isModified("password")){
        this.password = await bcrypt.hash(this.password, 10)
    }
});

userSchema.methods.comparePassword = async function (password){
    return bcrypt.compare(this.password, password)
}

userSchema.methods.generateAccessToken = async function () {
    return jwt.sign({
        _id: this._id,
        username: this.userName,
        email: this.email,
        check: this.isVerified 
    }, process.env.ACCESS_TOKEN_SECRET, { expiresIn: process.env.ACCESS_TOKEN_EXPIRY})
}

userSchema.methods.generateRefreshToken = async function () {
    return jwt.sign({
        _id: this._id,
        check: this.isVerified 
    }, process.env.REFRESH_TOKEN_SECRET, { expiresIn: process.env.REFRESH_TOKEN_EXPIRY})
}
export const User = mongoose.model("User", userSchema);