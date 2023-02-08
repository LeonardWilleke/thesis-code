#include <math.h>  // for fabs()
#include <float.h> // for DBL_MIN
#include "config.h"
#include "model.h"

#define V_MIN (0.1)
#define EVENT_EPSILON (1e-10)


void setStartValues(ModelInstance *comp) {
    M(v)         =  0;
    M(g)         = -9.81;
    M(a_drag)    =  0;
    M(a_tot)     =  M(g) + M(a_drag);
}

Status calculateValues(ModelInstance *comp) {
    M(a_tot)     =  M(g) + M(a_drag);
    return OK;
    
}

Status getFloat64(ModelInstance* comp, ValueReference vr, double *value, size_t *index) {
    switch (vr) {
        case vr_time:
            value[(*index)++] = comp->time;
            return OK;
        case vr_v:
            value[(*index)++] = M(v);
            return OK;
        case vr_der_v:
        case vr_a_tot:
            value[(*index)++] = M(a_tot);
            return OK;
        case vr_g:
            value[(*index)++] = M(g);
            return OK;
        case vr_a_drag:
            value[(*index)++] = M(a_drag);
            return OK;
        default:
            logError(comp, "Get Float64 is not allowed for value reference %u.", vr);
            return Error;
    }
}

Status setFloat64(ModelInstance* comp, ValueReference vr, const double *value, size_t *index) {
    switch (vr) {

        case vr_v:
            M(v) = value[(*index)++];
            return OK;
        case vr_der_v:
        case vr_a_tot:
            M(a_tot) = value[(*index)++];
            return OK;
        case vr_g:
            M(g) = value[(*index)++];
            return OK;
        case vr_a_drag:
            M(a_drag) = value[(*index)++];
            return OK;

        default:
            logError(comp, "Unexpected value reference: %u.", vr);
            return Error;
    }
}

Status getOutputDerivative(ModelInstance *comp, ValueReference valueReference, int order, double *value) {

    if (order != 1) {
        logError(comp, "The output derivative order %d for value reference %u is not available.", order, valueReference);
        return Error;
    }

    switch (valueReference) {
    case vr_v:
        *value = M(a_tot);
        return OK;
    default:
        logError(comp, "The output derivative for value reference %u is not available.", valueReference);
        return Error;
    }
}

void eventUpdate(ModelInstance *comp) {

    if (false) {
    
    } else {
        comp->valuesOfContinuousStatesChanged = false;
    }

    comp->nominalsOfContinuousStatesChanged = false;
    comp->terminateSimulation  = false;
    comp->nextEventTimeDefined = false;
}

void getContinuousStates(ModelInstance *comp, double x[], size_t nx) {
    UNUSED(nx);
    x[0] = M(v);
}

void setContinuousStates(ModelInstance *comp, const double x[], size_t nx) {
    UNUSED(nx);
    M(v) = x[0];
}

void getDerivatives(ModelInstance *comp, double dx[], size_t nx) {
    UNUSED(nx);
    dx[0] = M(a_tot);
}

void getEventIndicators(ModelInstance *comp, double z[], size_t nz) {

    UNUSED(nz);
    UNUSED(comp);
    UNUSED(z);

}
