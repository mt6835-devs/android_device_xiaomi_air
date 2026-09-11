/*
 * SPDX-FileCopyrightText: 2026 The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#define LOG_TAG "AntiFlickerService"
#include "AntiFlicker.h"
#include <android-base/file.h>
#include <android-base/logging.h>
#include <android-base/properties.h>

using android::base::ReadFileToString;
using android::base::WriteStringToFile;
using android::base::SetProperty;

namespace aidl {
namespace vendor {
namespace lineage {
namespace livedisplay {

static constexpr const char* kDCPath =
        "/sys/class/mi_display/disp-DSI-0/dc_status";

ndk::ScopedAStatus AntiFlicker::getEnabled(bool* _aidl_return) {
    std::string tmp;

    if (!ReadFileToString(kDCPath, &tmp)) {
        LOG(ERROR) << "Failed to read from " << kDCPath;
        return ndk::ScopedAStatus::fromExceptionCode(EX_UNSUPPORTED_OPERATION);
    }

    *_aidl_return = tmp.find("1") != std::string::npos;
    return ndk::ScopedAStatus::ok();
}

ndk::ScopedAStatus AntiFlicker::setEnabled(bool enabled) {
    SetProperty("persist.vendor.dc_backlight.enable", enabled ? "true" : "false");
    std::string value = enabled ? "1" : "0";

    if (!WriteStringToFile(value, kDCPath, true)) {
        LOG(ERROR) << "Failed to write to " << kDCPath;
        return ndk::ScopedAStatus::fromExceptionCode(EX_UNSUPPORTED_OPERATION);
    }

    return ndk::ScopedAStatus::ok();
}

}  // namespace livedisplay
}  // namespace lineage
}  // namespace vendor
}  // namespace aidl
