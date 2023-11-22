
    # ----------
    # TODO 5: FRESNEL
    #
    # In case we don't use fresnel, get reflectivity k_r directly using:
    reflectivity = mat.mirror_reflectivity
    # Otherwise, calculate k_r using Schlick’s approximation
    if mat.use_fresnel:
        # calculate R_0: R_0 = ((n1 - n2) / (n1 + n2))^2
        # Here n1 is the IOR of air, so n1 = 1
        # n2 is the IOR of the object, you can read it from the material property using: mat.ior
        # FILL IN YOUR CODE
        #
        R_0 = (((1-mat.ior)/(1+mat.ior))**2)
        #
        # Calculate reflectivity k_r = R_0 + (1 - R_0) (1 - cos(theta))^5 where theta is the incident angle.
        # REPLACE WITH YOUR CODE reflectivity = mat.mirror_reflectivity
        # Use the line below after checkpoint 4 is rendered
        k_reflectivity = R_0 + (1 - R_0) * ((1 - (np.cos(ray_dir.dot(hit_norm))))**5) 
    #
    # Re-run this script, and render the scene to check your result with Checkpoint 5.
    # ----------

    # ----------
    # TODO 4: RECURSION AND REFLECTION
    # If the depth is greater than zero, generate a reflected ray from the current x
    # If the depth is greater than zero, generate a reflected ray from the current intersection point 
    # using the direction D_reflect to determine the color contribution L_reflect.  
    # Multiply L_reflect by the reflectivity k_r, and then combine the result with the pixel color.
    #
    # Similar to how we handle shadow ray casting, it's important to account for self-occlusion in this context as well.
    # Remember to update depth at the end!
    if depth > 0:
        # Get the direction for reflection ray
        # D_reflect = D - 2 (D dot N) N
        # FILL IN YOUR CODE
        #
        # by checking what the ray_orig entails by print(ray_orig) it is apparent that
        # it is the camera as it's output is the same with the camera's location in blender
        # so the ray D that hits the object must be ray_dir as it is the ray from the origin
        # N is the hit location's normal vector and ray_dir and hit_norm are already normalized
        # by taking ray_dir and hit_norm's dot product, the angle between them is found
        # multiplying the angle by the normal vector also creates a vector, multiplying it by 2
        # and subtracting it from the ray_dir should give us the vector that is reflected
        # 
        D_reflect = ray_dir - 2 * (ray_dir.dot(hit_norm)) * hit_norm
        # Recursively trace the reflected ray and store the return value as a color L_reflect
        # reflect_color = np.zeros(3) 
        # REPLACE WITH YOUR CODE
        # making new origin because of self-occlusion
        new_orig = hit_loc + eps * D_reflect
        L_reflect = 0
        L_reflect += RT_trace_ray(scene, new_orig, D_reflect, lights, depth-1)
        # Add reflection to the final color: k_r * L_reflect
        color += reflectivity * L_reflect
        #
        # Re-run this script, and render the scene to check your result with Checkpoint 4.
        # ----------

        # ----------
        # TODO 6: TRANSMISSION
        #
        # If the depth is greater than zero, generate a transmitted ray from the current 
        # point of intersection using the direction D_transmit to calculate the color contribution L_transmit. 
        # Multiply this by (1 - k_r) * mat.transmission, and then add the result into the pixel color.
        #
        # Ensure that the refractive indices (n1 and n2) are assigned based on the media through which the ray is passing (as specified by ray_inside_object)
        # Use the refractive index of the object (mat.ior) and set the refractive index of air as 1
        # Proceed with the calculation of D_transmit only if the value under the square root is positive.
        # 
        # Since this part is already in the if statement, there is no need for the "if (depth > 0)"
        # Transmitted ray should have the same direction as the original ray, which is ray_dir
        # The current point of interection is hit_loc and the normal vector is hit_norm
        # D_transmit = D * n1/n2 - N * (n1/n2 * D * N + sqrt(1-(n1/n2)^2 * (1- (D * N)^2)))
        # Since there is no transmitted ray on the case the inside of the sqrt is negative, it is checked first
        if mat.transmission > 0:
            # FILL IN YOUR CODE
                # Add transmission to the final color: (1 - k_r) * L_transmit
                sn = 0
                if ray_inside_object:
                    sn = 1/mat.ior
                else:
                    sn = mat.ior/1
                root_val = (1 - ((sn**2) * (1 - ((ray_dir.dot(hit_norm))**2))))
                if root_val > 0:
                    D_transmit = ray_dir * sn - hit_norm * (sn * ray_dir.dot(hit_norm) + sqrt(root_val))
                    new_orig = hit_loc - hit_norm * eps
                    L_transmit = 0
                    L_transmit += RT_trace_ray(scene, new_orig, D_transmit, lights, depth-1)
                    color += (1 - k_reflectivity) * mat.transmission * L_transmit
                # np.zeros(3) REPLACE WITH YOUR CODE
    #
    # Re-run this script, and render the scene to check your result with Checkpoint 6.
    # ----------
