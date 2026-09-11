/*
 * SPDX-FileCopyrightText: 2026 The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#define LOG_TAG "SunlightEnhancementService"
#include "SunlightEnhancement.h"
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

static constexpr const char* kHBMPath =
        "/sys/class/mi_display/disp-DSI-0/disp_param";

ndk::ScopedAStatus SunlightEnhancement::getEnabled(bool* _aidl_return) {
    std::string tmp;

    if (!ReadFileToString(kHBMPath, &tmp)) {
        LOG(ERROR) << "Failed to read from " << kHBMPath;
        return ndk::ScopedAStatus::fromExceptionCode(EX_UNSUPPORTED_OPERATION);
    }

    *_aidl_return = tmp.find("hbm[01]: 1") != std::string::npos;
    return ndk::ScopedAStatus::ok();
}

ndk::ScopedAStatus SunlightEnhancement::setEnabled(bool enabled) {
    SetProperty("vendor.hbm.enable", enabled ? "true" : "false");
    std::string value = "1 ";
    value += enabled ? "1" : "0";

    if (!WriteStringToFile(value, kHBMPath, true)) {
        LOG(ERROR) << "Failed to write to " << kHBMPath;
        return ndk::ScopedAStatus::fromExceptionCode(EX_UNSUPPORTED_OPERATION);
    }

    return ndk::ScopedAStatus::ok();
}

}  // namespace livedisplay
}  // namespace lineage
}  // namespace vendor
}  // namespace aidl
