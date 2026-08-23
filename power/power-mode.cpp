/*
 * Copyright (C) 2021 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <aidl/android/hardware/power/BnPower.h>
#include <android-base/file.h>
#include <android-base/logging.h>

namespace aidl {
namespace google {
namespace hardware {
namespace power {
namespace impl {
namespace pixel {

using ::aidl::android::hardware::power::Mode;
using ::android::base::WriteStringToFile;

#define DOUBLE_TAP_NODE "/proc/tp_gesture"

bool isDeviceSpecificModeSupported(Mode type, bool* _aidl_return) {
    switch (type) {
        case Mode::DOUBLE_TAP_TO_WAKE:
            *_aidl_return = true;
            return true;
        default:
            return false;
    }
}

bool setDeviceSpecificMode(Mode type, bool enabled) {
    switch (type) {
        case Mode::DOUBLE_TAP_TO_WAKE: {
            if (!WriteStringToFile(enabled ? "1" : "0",
                                   DOUBLE_TAP_NODE,
                                   true)) {
                LOG(ERROR) << "Failed to write "
                           << (enabled ? "1" : "0")
                           << " to " << DOUBLE_TAP_NODE;
                return false;
            }

            LOG(INFO) << "Double Tap to Wake "
                      << (enabled ? "enabled" : "disabled");
            return true;
        }
        default:
            return false;
    }
}

}  // namespace pixel
}  // namespace impl
}  // namespace power
}  // namespace hardware
}  // namespace google
}  // namespace aidl
